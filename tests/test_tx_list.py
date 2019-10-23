from tests.helpers import TorinakuInstance


def test__simple():
    with TorinakuInstance() as instance:
        instance.send("\r")
        instance.expect("Transaction Browser")


def create_simple_tx(instance):
    instance.expect("Transaction Editor")
    instance.send("\t\t\t")  # Creator Account ID field
    instance.send("example@exampledomain")
    instance.send("\t" * 12 + "\r")  # "Save & Go back" button
    instance.expect("example@exampledo")  # Clipped for 80x25 screens


def test__create__simple():
    with TorinakuInstance() as instance:
        instance.send("\r")
        instance.expect("Transaction Browser")
        instance.send("\t\t\r")
        create_simple_tx(instance)


def test__edit__simple():
    with TorinakuInstance() as instance:
        instance.send("\r")
        instance.expect("Transaction Browser")
        instance.send("\t\t\r")
        create_simple_tx(instance)
        instance.send("\t\t\r")
        instance._dump_display()
        instance.send("\t\t\t")
        instance.send_backspace(100)
        instance.send("example2@exampledomain")
        instance._dump_display()
        instance.send("\t" * 12 + "\r")
        instance.expect("example2@exampled")
