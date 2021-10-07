import io
from math import floor
from pathlib import Path
from typing import BinaryIO, List

import qrcode
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from model.card import Card


class Template:
    def __init__(self,
                 image_path: Path,
                 card_size=(50 * mm, 50 * mm),
                 min_indent=(3 * mm, 3 * mm)) -> None:
        self.image_path = image_path
        self.card_size = card_size
        self.min_indent = min_indent

    def make_tokens(self, cards: List[Card], sink: BinaryIO, paper_size=A4):
        num_cols = self._get_num_cols(paper_size)
        num_rows = self._get_num_rows(paper_size)

        c = canvas.Canvas(sink, pagesize=paper_size)

        idx = 0
        while idx < len(cards):
            tags_on_page = min(num_cols * num_rows, len(cards) - idx)
            page_cards = cards[idx:idx + tags_on_page]
            self._make_page(c, page_cards, lambda item: ImageReader(self.image_path.joinpath(item.image_source)),
                            1 * mm, paper_size, True, True, False)

            self._make_page(c, page_cards, self._create_qr_img, 12 *
                            mm, paper_size, False, False, True)
            idx += tags_on_page

        c.save()

    def _create_qr_img(self, card: Card):
        img = qrcode.make(
            "https://paperplay.eu/" + card.id,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=16,
            border=1,
            version=3)
        output = io.BytesIO()
        img.save(output, format='png')
        output.seek(0)
        return ImageReader(output)

    def _get_indent(self, pagesize, num_rows, num_cols):
        return [(pagesize[0] - num_cols * self.card_size[0]) / 2, (pagesize[1] - num_rows * self.card_size[1]) / 2]

    def _get_num_cols(self, pagesize):
        return floor((pagesize[0] - self.min_indent[0] * 2) / self.card_size[0])

    def _get_num_rows(self, pagesize):
        return floor((pagesize[1] - self.min_indent[1] * 2) / self.card_size[1])

    def _make_page(self, canvas, cards, img_func, padding, pagesize, l2r=True, frame=True, text=True):
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
                    canvas.drawImage(img_func(card), posx + padding, posy +
                                     padding, self.card_size[0] - 2*padding, self.card_size[1] - 2*padding)
                    if text:
                        canvas.drawCentredString(
                            posx + self.card_size[0] / 2, posy + 10, card.id)
                    if l2r:
                        posx += self.card_size[0]
                    else:
                        posx -= self.card_size[0]
                posy -= self.card_size[1]
        except StopIteration:
            pass
        canvas.showPage()
