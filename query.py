import requests
import json

class APIMappings:
    aspect_map = None
    subcats_map = None

    @classmethod
    def mappings(cls):
        if cls.aspect_map is None and cls.subcats_map is None:
            cls.aspect_map, cls.subcats_map = read_data()
        return cls.aspect_map, cls.subcats_map


def get_anyheat_run(aspect, real_time=False, modded=False, version="v1.37+", seeded=False, place=1):
    request_string = "https://www.speedrun.com/api/v1/leaderboards/o1y9okr6/category/zd3xmmvd"
    request_params = {}
    
    aspect_map, subcats_map = APIMappings.mappings()

    request_params["var-" + aspect_map["variable_id"]] = aspect_map[aspect]

    if real_time:
        request_params["timing"] = "realtime"
    else:
        request_params["timing"] = "ingame"

    modded_id = "var-" + subcats_map["modded"]["id"]
    if modded:
        request_params[modded_id] = subcats_map["modded"]["values"]["modded"]
    else:
        request_params[modded_id] = subcats_map["modded"]["values"]["unmodded"]

    seeded_id = "var-" + subcats_map["seeded"]["id"]
    if seeded:
        request_params[seeded_id] = subcats_map["seeded"]["values"]["seeded"]
    else:
        request_params[seeded_id] = subcats_map["seeded"]["values"]["unseeded"]

    request_params["var-" + subcats_map["major_version"]["id"]] = subcats_map["major_version"]["values"][version]

    r = requests.get(request_string, params=request_params)
    print(r.url)
    results = r.json()

    runs = results["data"]["runs"]

    for run in runs:
        if run["place"] == place:
            return run["run"]

    return None

def read_data():
    with open('aspects.json') as f:
        aspect_map = json.load(f)['data']

    with open('subcats.json') as f:
        subcats_map = json.load(f)['data']

    return aspect_map, subcats_map