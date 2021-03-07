import serial
import click
import json
import struct
import os
import logging

@click.group()
@click.option("--port", help="Specify the serial device name")
@click.option("--baud", type=int, help="Specify the serial baud rate")
@click.option("--bits", type=int, help="Specify the number of data bits")
@click.option("--stop", type=int, help="Number of stop bits")
@click.option("--loglevel", help="Specify a logging level")
@click.pass_context
def cli(ctx, port, baud, bits, stop, loglevel):

	ctx.ensure_object(dict)
	ctx.obj["serial_settings"] = {}

	if "LPC_SETTINGS_PATH" in os.environ:
		with open(os.environ["LPC_SETTINGS_PATH"], "r") as f:
			settings = json.load(f)

		ctx.obj['serial_settings'] = settings
	
	if port is not None:
		ctx.obj['serial_settings']["port"] = port
	if baud is not None:
		ctx.obj['serial_settings']["baud"] = baud
	if bits is not None:
		ctx.obj['serial_settings']["data_bits"] = bits
	if stop is not None:
		ctx.obj['serial_settings']["stop_bits"] = stop


	if loglevel is not None:
		level = getattr(logging, loglevel.upper())
		logging.basicConfig(level=level)

@cli.command()
@click.argument('address', type=int)
@click.argument('bin_number', type=int)
@click.argument('red', type=int)
@click.argument('green', type=int)
@click.argument('blue', type=int)
@click.pass_context
def send(ctx, address, bin_number, red, green, blue):

	if address > 255:
		logging.error("Address must be less than a value of 255")
		return
	if bin_number > 16:
		logging.error("Address must be less than or equal to a value of 16")
		return
	if red > 255:
		logging.error("Red value must be less than a value of 255")
		return
	if green > 255:
		logging.error("Green value must be less than a value of 255")
		return
	if blue > 255:
		logging.error("Blue value must be less than a value of 255")
		return

	address_data = struct.pack("B", address)
	packet = struct.pack("BBBBc", bin_number, red, green, blue, "\n".encode("UTF8"))
	logging.debug("Sending the following packet: {} to controller address {}".format(packet, address))

	if ctx.obj['serial_settings']["data_bits"] == 7:
		data_bits = serial.SEVENBITS
	elif ctx.obj['serial_settings']["data_bits"] == 6:
		data_bits = serial.SIXBITS
	elif ctx.obj['serial_settings']["data_bits"] == 5:
		data_bits = serial.FIVEBITS
	else:
		data_bits = serial.EIGHTBITS

	if ctx.obj['serial_settings']["stop_bits"] == 2:
		stop_bits = serial.STOPBITS_TWO
	else:
		stop_bits = serial.STOPBITS_ONE

	if ctx.obj['serial_settings']["parity"].lower() == "odd":
		parity = serial.PARITY_ODD
	elif ctx.obj['serial_settings']["parity"].lower() == "even":
		parity = serial.PARITY_EVEN
	elif ctx.obj['serial_settings']["parity"].lower() == "mark":
		parity = serial.PARITY_MARK
	else:
		parity = serial.PARITY_NONE

	# Use parity bit for 9 bit master/slave communication
	ser = serial.Serial(ctx.obj["serial_settings"]["port"], int(ctx.obj["serial_settings"]["baud"]), bytesize=data_bits, stopbits=stop_bits, parity=serial.PARITY_MARK)
	ser.write(address_data)
	ser.close()

	ser = serial.Serial(ctx.obj["serial_settings"]["port"], int(ctx.obj["serial_settings"]["baud"]), bytesize=data_bits, stopbits=stop_bits, parity=serial.PARITY_SPACE)
	ser.write(packet)
	ser.close()

if __name__ == "__main__":
	cli(obj={})