import serial
import click
import json
import struct
import os
import logging

@click.group()
@click.option("--port", help="Specify the serial device name")
@click.option("--baud", default=115200, help="Specify the serial baud rate")
@click.option("--bits", default=8, help="Specify the number of data bits")
@click.option("--stop", default=1, help="Number of stop bits")
@click.pass_context
def cli(ctx, port, baud, bits, stop):

	if "LPC_SETTINGS_PATH" in os.environ:
		with open(os.environ["LPC_SETTINGS_PATH"], "r") as f:
			settings = json.load(f)

	ctx.obj['serial_settings'] = settings

@cli.command()
@click.pass_context
@click.argument('address', type=int)
@click.argument('bin_number', type=int)
@click.argument('red', type=int)
@click.argument('green', type=int)
@click.argument('blue', type=int)
def send(ctx, address, bin_number, red, green, blue):
	packet = struct.pack("BBBBBc", address, bin_number, red, green, blue, "\n".encode("UTF8"))
	logging.debug("Sending the following packet: {} to Address {}".format(packet, address))
	click.echo(packet)


if __name__ == "__main__":
	cli(obj={})