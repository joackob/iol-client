from iol_client.utils import iol_decoder_hook


def test_iol_decoder_hook():
    date_str = "2023-11-24T17:00:22.082Z"
    date_json = {"fecha": date_str}
    date_res = iol_decoder_hook(date_json)["fecha"]
    assert date_res.year == 2023
