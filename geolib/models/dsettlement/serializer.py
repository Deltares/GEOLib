import logging
from datetime import datetime

from jinja2 import Environment, PackageLoader

from geolib import __version__ as glversion
from geolib.models.serializers import BaseSerializer

ENV = Environment(loader=PackageLoader("geolib.models.dsettlement"))


class DSettlementInputSerializer(BaseSerializer):
    """Test"""

    def render(self) -> str:
        self.ds.update(dict(timestamp=datetime.now()))
        self.ds.update(dict(glversion=glversion))
        self.ds.update(dict(glversion=glversion))
        template = ENV.get_template("input.sli.j2")

        logging.warning(self.ds["version"])
        logging.warning(type(self.ds["version"]))

        return template.render(self.ds)
