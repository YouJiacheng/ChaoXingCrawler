import os
from fpdf import FPDF


class FPDF_fixed(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.buffer = bytearray()

    def _out(self, s):
        if(self.state == 2):  # 正在生成某一页
            # 兼容原代码，在一页内继续使用字符串，这会使生成页面内容有平方开销，但对于从图片生成pdf是无所谓的，因为页面内容仅是对图片资源的引用，而图片资源是单独附加的
            if isinstance(s, bytes):
                s = s.decode('latin1')
            elif not isinstance(s, str):
                s = str(s)
            self.pages[self.page] += s + '\n'
        else:
            if not isinstance(s, bytes):
                if not isinstance(s, str):
                    s = str(s)
                s = s.encode('latin1')
            self.buffer += s + b'\n'

    def output(self, name=''):
        if(self.state < 3):
            self.close()
        with open(name, 'wb') as f:
            f.write(self.buffer)


if __name__ == '__main__':
    pdf = FPDF_fixed()
    for page in range(1, 389):
        pdf.add_page()
        pdf.image(f'download/{page}.png', x=0, y=0, w=210, h=297)
    pdf.output('output.pdf')
