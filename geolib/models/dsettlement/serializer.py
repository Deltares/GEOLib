from datetime import datetime

from jinja2 import Environment, PackageLoader

from geolib import __version__ as glversion
from geolib.models.serializers import BaseSerializer

ENV = Environment(loader=PackageLoader("geolib.models.dsettlement"), trim_blocks=True)


class DSettlementInputSerializer(BaseSerializer):
    def render(self) -> str:
        self.ds.update(dict(timestamp=datetime.now()))
        self.ds.update(dict(glversion=glversion))
        template = ENV.get_template("input.sli.j2")

        return template.render(self.ds)
