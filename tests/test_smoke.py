def test_docs_page_opens(client):
    response = client.get("/docs")
    assert response.status_code == 200