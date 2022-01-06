from chroniccrawler.models import *


def get_all_nodes_to_detect_landmark():
    return NodeOfLane.objects.all()


def get_all_landmark_nodes_as_dict():
    landmark_nodes = LandmarkNode.objects.all()

    nodedict = {}

    for n in landmark_nodes:
        nodedict[n.node_id] = n

    return nodedict


def detect_and_set(nodes, nodedict):
    LandmarkOfLane.objects.all().delete()

    for node in nodes:
        try:
            landmark = nodedict[node.node_id]
        except:
            continue

        landmarkoflane, created = LandmarkOfLane.objects.get_or_create(route_key=node.route_key)

        landmarkoflane.landmark_keys.add(landmark)


def do_landmark():
    nodes = get_all_nodes_to_detect_landmark()
    nodedict = get_all_landmark_nodes_as_dict()

    detect_and_set(nodes, nodedict)
