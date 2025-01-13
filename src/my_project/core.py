import cowsay


def cowsay_nice_template() -> str:
    return cowsay.get_output_string("cow", "Nice Project Template!")
