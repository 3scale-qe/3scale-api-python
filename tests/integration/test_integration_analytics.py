import pytest


def create_resources(service, proxy, metric_params):
    metric = service.metrics.create(params=metric_params)
    rule_params = dict(http_method='GET', metric_id=metric['id'], delta=1,
                       pattern=f'/anything/{metric["system_name"]}')
    rule = proxy.mapping_rules.create(params=rule_params)
    return rule['pattern']


def do_request(client, path):
    for _ in range(2):
        response = client.get(path=path)
        assert response.status_code == 200


def test_should_get_analytics_by_service(api, service, proxy, metric_params,
                                         apicast_http_client):
    path = create_resources(service, proxy, metric_params)
    do_request(apicast_http_client, path)
    data = api.analytics.list_by_service(service)
    assert data['total'] == 2

