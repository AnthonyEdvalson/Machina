import pytest

from tools.config.configloader import ConfigLoader
from vertex.resources import Resources
from vertex.vertex.logic import Logic, NoWorkers


def conf():
    return ConfigLoader("tests/config.json", "default").load_json()


def test_add_node():
    logic, res = setup_default_logic()

    with pytest.raises(AssertionError):
        logic.add_node("name1", 123, res)

    workers = logic.get_workers()

    assert len(workers) == 2
    assert workers["name2"].server_port == 123
    assert workers["name2"].resources == res
    assert workers["name2"].leases == []


def test_allocate_worker():
    config = conf()
    config.alter("layers/layer1/resources", Resources(5, 5, 5, 5, 5).as_dict())  # make layer1 use all resources

    logic, res = setup_default_logic(Logic(config))

    with pytest.raises(KeyError):
        logic.allocate_worker("xxx")

    logic.allocate_worker("name1")
    worker = logic.get_workers()["name1"]
    assert len(worker.leases) == 1
    assert worker.leases[0].layer == "layer1"
    assert worker.leases[0].resources == res

    logic.allocate_worker("name2")
    worker = logic.get_workers()["name2"]
    assert len(worker.leases) == 1
    assert worker.leases[0].layer == "layer2"
    assert worker.leases[0].resources != res


def test_call():
    logic = Logic(conf())  # setup logic

    # try to connect to layer1, an error should be thrown because there are no nodes running layer1
    with pytest.raises(NoWorkers):
        logic.call("layer1")

    logic, _ = setup_default_logic(logic)  # add some nodes with some resources

    # update lease queue, which will allocate leases to the nodes by default
    logic.update_lease_queue()

    # try to connect to layer1 again, still fails because nodes have not notified vertex that they are set up yet
    with pytest.raises(NoWorkers):
        logic.call("layer1")

    logic.activate_lease(logic.get_worker("name1").leases[0].uid)

    worker = logic.call("layer1")

    assert worker.get_layer("layer1") is not None
    assert worker.name in ["name1", "name2"]
    assert worker.get_layer("layer1").resources == Resources(**logic.config["layers/layer1/resources"])


def setup_default_logic(logic=None) -> (Logic, Resources):
    logic = Logic(conf()) if logic is None else logic

    res = Resources(5, 5, 5, 5, 5)
    logic.add_node("name1", 123, res)
    logic.add_node("name2", 123, res)

    return logic, res
