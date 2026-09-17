import sys
import httpx
import uuid

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print(f"Connecting to FastAPI backend at {BASE_URL}...")
    client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] 1. Backend health check OK")

    # 2. Authenticate test user
    test_email = f"crud_tester_{uuid.uuid4().hex[:6]}@darukaa.earth"
    test_password = "SecurePassword123!"

    reg_res = client.post("/auth/register", json={"email": test_email, "password": test_password})
    assert reg_res.status_code == 201, f"Register failed: {reg_res.text}"
    print(f"[PASS] 2. Registered test user: {test_email}")

    login_res = client.post("/auth/login", json={"email": test_email, "password": test_password})
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token_data = login_res.json()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[PASS] 3. Obtained JWT token")

    # 3. Verify public reads work without token
    p_list_res = client.get("/projects")
    assert p_list_res.status_code == 200, f"Public GET /projects failed: {p_list_res.text}"
    s_list_res = client.get("/sites")
    assert s_list_res.status_code == 200, f"Public GET /sites failed: {s_list_res.text}"
    print("[PASS] 4. Public GET /projects and GET /sites work without auth")

    # 4. Verify unauthenticated writes are rejected (401)
    unauth_p = client.post("/projects", json={"name": "Fail", "type": "carbon"})
    assert unauth_p.status_code == 401, f"Expected 401 for unauth project create, got {unauth_p.status_code}"

    unauth_s = client.post("/sites", json={"name": "Fail", "projectId": "fake", "geometry": {"type": "Polygon", "coordinates": []}})
    assert unauth_s.status_code == 401, f"Expected 401 for unauth site create, got {unauth_s.status_code}"

    unauth_del = client.delete("/projects/non-existent")
    assert unauth_del.status_code == 401, f"Expected 401 for unauth project delete, got {unauth_del.status_code}"
    print("[PASS] 5. Unauthenticated write endpoints properly reject with 401")

    # 5. Project CRUD
    proj_payload = {
        "name": f"Amazon Restoration Test {uuid.uuid4().hex[:4]}",
        "type": "carbon",
        "status": "active",
        "description": "High-integrity tropical reforestation project.",
    }
    create_proj_res = client.post("/projects", json=proj_payload, headers=headers)
    assert create_proj_res.status_code == 201, f"Create project failed: {create_proj_res.text}"
    proj_data = create_proj_res.json()
    project_id = proj_data["id"]
    assert proj_data["name"] == proj_payload["name"]
    assert proj_data["type"] == "carbon"
    assert proj_data["status"] == "active"
    assert "siteCount" in proj_data and proj_data["siteCount"] == 0
    assert "lastUpdated" in proj_data
    print(f"[PASS] 6. Created Project: {project_id} ({proj_data['name']})")

    # GET /projects/{id}
    get_proj_res = client.get(f"/projects/{project_id}")
    assert get_proj_res.status_code == 200, f"GET project failed: {get_proj_res.text}"
    assert get_proj_res.json()["id"] == project_id
    print(f"[PASS] 7. GET /projects/{project_id} retrieved successfully")

    # PATCH /projects/{id}
    patch_proj_res = client.patch(
        f"/projects/{project_id}",
        json={"status": "monitoring", "description": "Updated monitoring description"},
        headers=headers,
    )
    assert patch_proj_res.status_code == 200, f"PATCH project failed: {patch_proj_res.text}"
    patched_data = patch_proj_res.json()
    assert patched_data["status"] == "monitoring"
    assert patched_data["description"] == "Updated monitoring description"
    print(f"[PASS] 8. PATCH /projects/{project_id} updated successfully")

    # 6. Site CRUD with GeoJSON Polygon
    test_polygon = {
        "type": "Polygon",
        "coordinates": [
            [
                [-60.0, -3.0],
                [-59.9, -3.0],
                [-59.9, -2.9],
                [-60.0, -2.9],
                [-60.0, -3.0],
            ]
        ],
    }

    site_payload = {
        "name": "Sector Alpha Plot",
        "projectId": project_id,
        "siteType": "Reforestation",
        "geometry": test_polygon,
    }
    create_site_res = client.post("/sites", json=site_payload, headers=headers)
    assert create_site_res.status_code == 201, f"Create site failed: {create_site_res.text}"
    site_data = create_site_res.json()
    site_id = site_data["id"]
    assert site_data["name"] == "Sector Alpha Plot"
    assert site_data["projectId"] == project_id
    assert site_data["siteType"] == "Reforestation"
    assert site_data["geometry"]["type"] == "Polygon"
    assert len(site_data["geometry"]["coordinates"][0]) == 5
    assert "createdAt" in site_data
    print(f"[PASS] 9. Created Site: {site_id} with GeoJSON Polygon")

    # GET /sites/{id}
    get_site_res = client.get(f"/sites/{site_id}")
    assert get_site_res.status_code == 200, f"GET site failed: {get_site_res.text}"
    assert get_site_res.json()["geometry"]["type"] == "Polygon"
    print(f"[PASS] 10. GET /sites/{site_id} returned valid GeoJSON")

    # GET /sites?project_id=...
    filter_site_res = client.get(f"/sites?project_id={project_id}")
    assert filter_site_res.status_code == 200, f"Filter sites failed: {filter_site_res.text}"
    filtered_sites = filter_site_res.json()
    assert any(s["id"] == site_id for s in filtered_sites)
    print(f"[PASS] 11. GET /sites?project_id={project_id} returned {len(filtered_sites)} matching sites")

    # Verify project siteCount is now 1
    proj_with_count = client.get(f"/projects/{project_id}").json()
    assert proj_with_count["siteCount"] == 1, f"Expected siteCount == 1, got {proj_with_count['siteCount']}"
    print("[PASS] 12. Project siteCount correctly reflects 1 associated site")

    # 7. Site validation errors
    # Non-existent project
    bad_proj_site = client.post(
        "/sites",
        json={"name": "Bad", "projectId": "non-existent-proj", "geometry": test_polygon},
        headers=headers,
    )
    assert bad_proj_site.status_code == 404, f"Expected 404 for non-existent project, got {bad_proj_site.status_code}"
    print("[PASS] 13. Site creation with non-existent project returned 404")

    # Invalid geometry
    bad_geom_site = client.post(
        "/sites",
        json={"name": "Bad", "projectId": project_id, "geometry": {"type": "Point", "coordinates": [0, 0]}},
        headers=headers,
    )
    assert bad_geom_site.status_code == 400, f"Expected 400 for non-polygon geometry, got {bad_geom_site.status_code}"
    print("[PASS] 14. Site creation with non-Polygon geometry returned 400")

    # 8. Cascade delete verification
    del_proj_res = client.delete(f"/projects/{project_id}", headers=headers)
    assert del_proj_res.status_code == 204, f"Delete project failed: {del_proj_res.status_code}"
    print(f"[PASS] 15. Deleted project {project_id} (204 No Content)")

    # Confirm project is gone
    assert client.get(f"/projects/{project_id}").status_code == 404
    print("[PASS] 16. Confirmed project returns 404 after deletion")

    # Confirm site was cascade deleted
    assert client.get(f"/sites/{site_id}").status_code == 404
    print("[PASS] 17. Confirmed site was CASCADE DELETED and returns 404")

    print("\n==========================================")
    print("ALL 17 CRUD & AUTH VERIFICATION TESTS PASSED!")
    print("==========================================")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"[ERROR] Test execution failed: {e}")
        sys.exit(1)
