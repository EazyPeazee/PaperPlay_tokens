import io
from math import floor
from pathlib import Path
from typing import BinaryIO, List

import qrcode
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

from model.card import Card


class Template:
    def __init__(self,
                 image_path: Path,
                 card_size: float = 50,
                 min_margin: float = 3,
                 qr_padding: float = 3,
                 img_padding: float = 2,
                 multiple_qr_codes: bool = False) -> None:
        self.image_path = image_path
        self.card_size = (card_size * mm, card_size * mm)
        self.min_margin = (min_margin * mm, min_margin * mm)
        self.qr_padding = qr_padding * mm
        self.img_padding = img_padding * mm
        self.multiple_qr_codes = multiple_qr_codes

    def make_tokens(self, cards: List[Card], sink: BinaryIO, paper_size=A4):
        num_cols = self._get_num_cols(paper_size)
        num_rows = self._get_num_rows(paper_size)

        c = canvas.Canvas(sink, pagesize=paper_size)

        idx = 0
        while idx < len(cards):
            tags_on_page = min(num_cols * num_rows, len(cards) - idx)
            page_cards = cards[idx:idx + tags_on_page]
            self._make_page(c, page_cards, lambda item: ImageReader(self.image_path.joinpath(item.image_source)),
                            self.img_padding, paper_size, True, True)

            self._make_page(c, page_cards, lambda card: self._create_qr_img(card, multi=self.multiple_qr_codes),
                            self.qr_padding, paper_size, False, True)
            idx += tags_on_page

        c.save()

    def _create_qr_img(self, card: Card, multi: bool = False):
        qrImg = qrcode.make(
            "https://paperplay.eu/" + card.id,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=16,
            border=4,
            version=3)
        if multi:
            img = Image.new('RGB', (2*qrImg.size[0],
                            2*qrImg.size[1]), (255, 255, 255))
            img.paste(qrImg, (0, 0))
            img.paste(qrImg, (qrImg.size[0], 0))
            img.paste(qrImg, (0, qrImg.size[1]))
            img.paste(qrImg, (qrImg.size[0], qrImg.size[1]))
        else:
            img = qrImg
        output = io.BytesIO()
        img.save(output, format='png')
        output.seek(0)
        return ImageReader(output)

    def _get_indent(self, pagesize, num_rows, num_cols):
        return [(pagesize[0] - num_cols * self.card_size[0]) / 2, (pagesize[1] - num_rows * self.card_size[1]) / 2]

    def _get_num_cols(self, pagesize):
        return floor((pagesize[0] - self.min_margin[0] * 2) / self.card_size[0])

    def _get_num_rows(self, pagesize):
        return floor((pagesize[1] - self.min_margin[1] * 2) / self.card_size[1])

    def _make_page(self, canvas, cards, img_func, padding, pagesize, l2r=True, frame=True):
        num_cols = self._get_num_cols(pagesize)
        num_rows = self._get_num_rows(pagesize)
        indent = self._get_indent(pagesize, num_rows, num_cols)
        it = iter(cards)
        canvas.setFont("Helvetica", 7)
        try:
            posy = pagesize[1] - self.card_size[1] - indent[1]
            for _ in range(num_rows):
                if l2r:
                    posx = indent[0]
                else:
                    posx = pagesize[0] - indent[0] - self.card_size[0]
                for _ in range(num_cols):
                    card = next(it)
                    if frame:
                        canvas.rect(
                            posx, posy, self.card_size[0], self.card_size[1])
                    canvas.drawImage(
                        img_func(card),
                        posx + padding,
                        posy + padding,
                        self.card_size[0] - 2*padding,
                        self.card_size[1] - 2*padding,
                        mask='auto')
                    if l2r:
                        posx += self.card_size[0]
                    else:
                        posx -= self.card_size[0]
                posy -= self.card_size[1]
        except StopIteration:
            pass
        canvas.showPage()
