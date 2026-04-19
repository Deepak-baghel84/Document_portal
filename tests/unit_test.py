import api.main as main
from fastapi.testclient import TestClient


client=TestClient(main.app)

file_path="Data//Resume.pdf"
def test_health_check():
    response=client.get("/health")
    assert response.status_code==200
    assert response.json()=={"status":"ok","message":"Service is healthy","device":"document-portal"}

# def test_analyze_document():
#     with open(file_path, "rb") as f:
#         response=client.post("/analyze", files={"file": f})
#     assert response.status_code==200
#     assert isinstance(response.json(), dict)

print("all okay")
