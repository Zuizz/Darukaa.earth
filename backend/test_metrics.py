import sys
import httpx
import uuid
from app.core.database import SessionLocal
from app.models.site import Site
from app.models.project import Project
from app.models.metric import SiteMetric

BASE_URL = "http://127.0.0.1:8000"


def run_metrics_verification():
    print(f"Connecting to FastAPI backend at {BASE_URL}...")
    client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    # 1. Health check
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] 1. Backend health check OK")

    # 2. Check existing sites
    sites_res = client.get("/sites")
    assert sites_res.status_code == 200, f"GET /sites failed: {sites_res.text}"
    sites = sites_res.json()
    assert len(sites) > 0, "No sites found to test metrics!"
    print(f"[PASS] 2. Found {len(sites)} existing sites in database")

    # 3. Test metrics on an existing seeded carbon site
    target_site = sites[0]
    site_id = target_site["id"]
    metrics_res = client.get(f"/sites/{site_id}/metrics")
    assert metrics_res.status_code == 200, f"GET /sites/{site_id}/metrics failed: {metrics_res.text}"
    data = metrics_res.json()

    print(f"[PASS] 3. GET /sites/{site_id}/metrics returned 200 OK")

    # Validate shape required by SiteDetail.jsx
    assert data["siteId"] == site_id, f"Expected siteId {site_id}, got {data['siteId']}"
    assert "type" in data and data["type"] in ["carbon", "biodiversity"], f"Invalid type: {data['type']}"
    assert 0 <= data["healthScore"] <= 100, f"Invalid healthScore: {data['healthScore']}"
    assert 0 <= data["healthTarget"] <= 100, f"Invalid healthTarget: {data['healthTarget']}"

    # Primary Metric
    pm = data["primaryMetric"]
    assert "label" in pm and "unit" in pm and "currentValue" in pm and "annualChange" in pm
    assert len(pm["trend"]) == 12, f"Expected 12 points in primary trend, got {len(pm['trend'])}"
    print(f"[PASS] 4. Primary metric '{pm['label']}' ({pm['unit']}): {pm['currentValue']} ({pm['annualChange']}) with 12 trend points")

    # Secondary Metric
    sm = data["secondaryMetric"]
    assert "label" in sm and "unit" in sm and "totalAnnual" in sm and "description" in sm
    assert len(sm["trend"]) == 12, f"Expected 12 points in secondary trend, got {len(sm['trend'])}"
    print(f"[PASS] 5. Secondary metric '{sm['label']}' ({sm['unit']}): {sm['totalAnnual']} with 12 trend points")

    # Supporting Metric
    sup = data["supportingMetric"]
    assert "label" in sup and "value" in sup and "change" in sup
    print(f"[PASS] 6. Supporting metric '{sup['label']}': {sup['value']} ({sup['change']})")

    # Months list
    assert len(data["months"]) == 12
    assert data["months"][0] == "Dec 23"
    assert data["months"][-1] == "Nov 24"
    print("[PASS] 7. 12-month calendar verified ('Dec 23' -> 'Nov 24')")

    # 4. Validate Indian phenology seasonal curve: summer dry dip vs monsoon flush
    # In carbon sites: month index 4 (Apr/May) should be lower than month index 7/8 (Jul/Aug)
    if data["type"] == "carbon":
        apr_may_canopy = min(pm["trend"][3], pm["trend"][4])
        jul_aug_canopy = max(pm["trend"][7], pm["trend"][8])
        assert jul_aug_canopy > apr_may_canopy, (
            f"Expected monsoon canopy ({jul_aug_canopy}) > dry season canopy ({apr_may_canopy})"
        )
        print(f"[PASS] 8. Seasonal phenology confirmed: Dry-season trough ({apr_may_canopy}%) < Monsoon flush ({jul_aug_canopy}%)")

    # 5. Create a biodiversity project and site to test biodiversity metric format
    reg_user = client.post(
        "/auth/register",
        json={"email": f"bio_tester_{uuid.uuid4().hex[:6]}@darukaa.earth", "password": "SecurePassword123!"},
    )
    user_token = client.post(
        "/auth/login",
        data={"username": reg_user.json()["email"], "password": "SecurePassword123!"},
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {user_token}"}

    bio_proj = client.post(
        "/projects",
        json={"name": "Western Ghats Biodiversity Test", "type": "biodiversity"},
        headers=headers,
    ).json()

    bio_site = client.post(
        "/sites",
        json={
            "name": "Shola Patch Alpha",
            "projectId": bio_proj["id"],
            "siteType": "biodiversity",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.5, 10.0], [76.6, 10.0], [76.6, 10.1], [76.5, 10.1], [76.5, 10.0]]],
            },
        },
        headers=headers,
    ).json()

    # Query metrics for newly created site (tests on-demand phenology generation and persistence)
    bio_metrics_res = client.get(f"/sites/{bio_site['id']}/metrics")
    assert bio_metrics_res.status_code == 200, f"GET bio metrics failed: {bio_metrics_res.text}"
    bio_data = bio_metrics_res.json()

    assert bio_data["type"] == "biodiversity"
    assert bio_data["primaryMetric"]["label"] == "Biodiversity Index"
    assert bio_data["secondaryMetric"]["label"] == "Species Observations"
    assert bio_data["supportingMetric"]["label"] == "Disturbance Index"
    assert len(bio_data["primaryMetric"]["trend"]) == 12
    assert len(bio_data["secondaryMetric"]["trend"]) == 12
    print(f"[PASS] 9. Newly created biodiversity site dynamically generated and returned 12-month metrics: {bio_data['primaryMetric']['currentValue']} pts")

    # 6. Test 404 on non-existent site
    bad_res = client.get("/sites/non-existent-site-id/metrics")
    assert bad_res.status_code == 404, f"Expected 404, got {bad_res.status_code}"
    print("[PASS] 10. Non-existent site properly returned 404 Not Found")

    # Clean up test project (cascade deletes test site and its metrics)
    client.delete(f"/projects/{bio_proj['id']}", headers=headers)
    assert client.get(f"/sites/{bio_site['id']}/metrics").status_code == 404
    print("[PASS] 11. Cascade deletion verified: metrics cleaned up when parent project was deleted")

    # 7. Verify direct Supabase database records
    db = SessionLocal()
    try:
        count = db.query(SiteMetric).count()
        assert count >= 24, f"Expected at least 24 metrics rows in DB, found {count}"
        print(f"[PASS] 12. Direct DB verification: {count} total site_metrics rows persisted in Supabase")
    finally:
        db.close()

    print("\n==========================================")
    print("ALL 12 METRICS & ANALYTICS VERIFICATION TESTS PASSED!")
    print("==========================================")


if __name__ == "__main__":
    try:
        run_metrics_verification()
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        sys.exit(1)
