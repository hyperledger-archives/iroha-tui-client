from tests.helpers import TorinakuInstance


def test__command__add():
    with TorinakuInstance() as instance:
        instance.send("\r\t\r" + "\t" * 7 + "\r")
        instance.expect("Add command")
        instance.send_movement("down", 1)
        instance.send("\r")
        instance.expect("Command Editor")
        instance.expect("Add Peer")
        instance.send("\t\t")
        instance.send("127.0.0.1:50051")
        instance.send("\t")
        instance.send("example_key")
        instance.send("\t\r")
        instance.expect("AddPeer")


def test__command__edit():
    with TorinakuInstance() as instance:
        instance.send("\r\t\r" + "\t" * 12 + "\r")
        instance.expect("Command Editor")
        instance.send("\t\t\t")
        instance.send_backspace(100)
        instance.send("exkey")
        instance.send("\t\t\r")
        instance.expect("exkey")
