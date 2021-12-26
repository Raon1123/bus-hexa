from chroniccrawler.models import LaneToTrack, NodeOfLane, PartOfLane, UlsanBus_NodeToTrack


def get_all_nodes_to_check():
    nodes = NodeOfLane.objects.all()
    return nodes


def group_by_lane_and_node(nodes):
    nodes = nodes.order_by('route_key', 'node_order')

    lanes = LaneToTrack.objects.all()

    lanes_and_nodes = {}
    
    for lane in lanes:
        lanes_and_nodes[lane.route_id] = [lane, []]

    for node in nodes:
        rid = node.route_key.route_id
        if rid in lanes_and_nodes:
            lanes_and_nodes[rid][1].append(node)

    new_lan = []

    for key in lanes_and_nodes:
        new_lan.append(lanes_and_nodes[key])

    return new_lan


def make_groups(lans):
    track_nodes_qset = UlsanBus_NodeToTrack.objects.all()
    track_nodes = [n.node_id for n in track_nodes_qset]

    groups = []

    for lan in lans:
        lane = lan[0]
        nodes = lan[1]

        group = [lane, []]

        first_node = nodes[0]

        for node in nodes[:-1]:
            if node.node_id[3:] in track_nodes: 
                # BEWARE! HARDCODED VALUE! NODE ID PREFIX MIGHT NOT BE 3 LETTERS IN [3:]!
                group[1].append([first_node, node])

        groups.append(group)

    return groups


def make_parts(groups):
    PartOfLane.objects.all().delete()    

    for group in groups:
        lane = group[0]
        pairs = group[1]
        counter = 0

        for pair in pairs:
            start = pair[0]
            end = pair[1]

            partname = lane.bus_name + "/" + str(start.node_order) + "~" + str(end.node_order)

            part = PartOfLane(lane_key=lane, first_node_key=start,
                last_node_key=end, part_name=partname, count=counter)

            part.save()

            counter = counter + 1

    return 0


def do_lanepart():
    lanes = get_all_nodes_to_check()

    lans = group_by_lane_and_node(lanes)

    groups = make_groups(lans)

    make_parts(groups)

    return 0
