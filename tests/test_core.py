from my_project import cowsay_nice_template


def test_core():
    assert "Nice Project Template!" in cowsay_nice_template()
