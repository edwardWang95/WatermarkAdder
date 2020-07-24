#!/usr/bin/env python3

"""
Watermarker.py

Provide a target pdf and target watermarker.pdf a from page to end page in the target pdf

Usage:

Add watermark to p1.pdf start page 10 to end page 15
./watermarker.py p1.pdf watermark.pdf --start 10 --end 15

./watermarker.py ~/Desktop/Atlas\ of\ Human\ Anatomy\ 7th\ Edition.pdf ~/Desktop/Atlas\ of\ Human\ Anatomy\ 7th\ Edition.pdf --start 10 --end 15
"""


import logging
import os
import sys

from reportlab.pdfgen import canvas
import PyPDF2
from PyPDF2 import PdfFileReader


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# TODO: Add argument for choosing output file: --output file_path
OUTPUT_FILE_NAME = "merged.pdf"
OUTPUT_FILE_PATH = '/'.join([os.getcwd(), 
							OUTPUT_FILE_NAME])


class WatermarkerException(Exception):
	"""Base class"""


class NotPDFException(Exception):
	"""Not a .pdf"""	


class MissingStartPageException(Exception):
	"""Missing start page number"""


class MissingEndPageException(Exception):
	"""Missing end page exception"""


class Watermarker:
	"""Add watermark to pdf"""

	def add_watermark(self, pdf_path, watermark_path, start_page, end_page):
		"""
		Add watermark to pdf from start to end page.
		If end page is not given then the last page of pdf is stopping point
		"""
		pdf_file = open(pdf_path,'rb')
		pdf = PyPDF2.PdfFileReader(pdf_path)
		LOG.debug("Opened pdf file")

		self.set_watermark_location(watermark_path)
		watermark_file = open(watermark_path,'rb')
		watermark_page = PyPDF2.PdfFileReader(watermark_file).getPage(0)
		LOG.debug("Got watermark pdf page")
		
		output_writer = PyPDF2.PdfFileWriter()
		merged_file = open(OUTPUT_FILE_PATH,'wb')
		LOG.debug(f'Output file: f{OUTPUT_FILE_PATH}')

		if not end_page:
			# set end page to last page in PDF
			end_page = self.get_pdf_size(pdf_path)

		for page_num in range(start_page, end_page):
			pdf_page = pdf.getPage(page_num)
			pdf_page.mergePage(watermark_page)
			
			output_writer.addPage(pdf_page)

		output_writer.write(merged_file)
		
		merged_file.close()
		pdf_file.close()
		watermark_file.close()
		LOG.debug(f'Closed files')
	
	@staticmethod
	def set_watermark_location(watermark_image_pdf_path):
		c = canvas.Canvas("watermark.pdf")
		# c.drawString(800, 720, "BIG ASS WATERMARK")
		c.drawImage('watermark.png', 180, 0, width=280, height=35)
		c.save()
		LOG.debug(f'Specify watermark page location')
	
	@staticmethod
	def get_pdf_size(pdf_path):
		"""Get total page size of pdf
		:param path: pdf path
		:return page size
		"""
		pdf_file = open(pdf_path,'rb')
		pdf_num = PdfFileReader(pdf_file).getNumPages()
		pdf_file.close()
		return pdf_num


def check_is_pdf(arg):
	"""
	Check if command line arg input is a type pdf
	"""
	return arg.endswith('.pdf')

if __name__ == "__main__":
	print("Welcome to Edward's watermarker.")

	pdf_path = sys.argv[1]
	check_is_pdf(pdf_path)
	print(f"Editing pdf:   {pdf_path}")

	watermarker_path = sys.argv[2]
	check_is_pdf(watermarker_path)
	print(f"Watermark pdf: {watermarker_path}")

	start_page = 0
	end_page = None

	if len(sys.argv) > 3:
		i = 3
		while i < len(sys.argv):
			LOG.debug(f'Arg type: {sys.argv[i]}')
			if sys.argv[i] == "--start":
				try:
					start_page = sys.argv[i + 1]
					print(f'Start page: {start_page}')
				except IndexError:
					raise MissingStartPageException()
			elif sys.argv[i] == "--end":
				try:
					end_page = sys.argv[i + 1]
					print(f'End page: {end_page}')
				except IndexError:
					raise MissingEndPageException()
			i = i + 2
	

	watermarker = Watermarker()
	watermarker.add_watermark(pdf_path,
							  watermarker_path,
							  start_page,
							  end_page)

	


