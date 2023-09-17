import base64
import itertools
from uuid import uuid4

import requests
from pydantic import BaseModel, Field


def guid():
    x = uuid4().hex
    while True:
        try:
            int(x[0])
            break
        except ValueError:
            x = x[1:]
    return x[:6]


class OutcomeNode(BaseModel):
    value: float
    desc: str = ""
    id: str = Field(default_factory=guid)

    @property
    def expected_value(self) -> float:
        return self.value

    def render(self) -> str:
        return self.id + "{{" + self.desc + "}}"

    def render_edge(self, parent) -> list[str]:
        if self.desc:
            return ["    " + parent.render() + " --> " + self.id + "{{" + self.desc + ": " + str(self.value) +  "}}"]
        else:
            return ["    " + parent.render() + " --> " + self.id + "{{" + str(self.value) +  "}}"]


class Chance(BaseModel):
    desc: str
    probability: float
    node: "DecisionNode | OutcomeNode"
    id: str = Field(default_factory=guid)

    @property
    def expected_value(self) -> float:
        match self.node:
            case DecisionNode():
                return max(
                    [round(decision.expected_value, 2) for decision in self.node.decisions]
                )
            case OutcomeNode():
                return self.node.value * self.probability
            case _:
                raise NotImplementedError()

    def render(self) -> str:
        return f"{self.id}[{self.desc}]"

    def render_edge(self, parent) -> list[str]:
        if parent is None:
            this = []
        else:
            this = ["    " + parent.render() + " --> " + f"|{round(self.probability, 3)}| " + self.render()]
        children = self.node.render_edge(self)
        return this + children


class ChanceNode(BaseModel):
    chances: list[Chance]
    desc: str = ""
    id: str = Field(default_factory=guid)

    @property
    def expected_value(self) -> float:
        return round(sum([chance.expected_value for chance in self.chances]), 2)

    def render(self) -> str:
        return f"{self.id}(( ))"

    def render_edge(self, parent) -> list[str]:
        if parent is None:
            this = []
        else:
            this = ["    " + parent.render() + " --> " + self.render()]
        children = list(itertools.chain(*[
            node.render_edge(self) for node in self.chances
        ]))
        return this + children


class Decision(BaseModel):
    desc: str
    node: ChanceNode
    id: str = Field(default_factory=guid)

    @property
    def expected_value(self) -> float:
        return self.node.expected_value

    def render(self) -> str:
        return self.id + f"[{self.desc}<br/>{self.expected_value}]"

    def render_edge(self, parent) -> list[str]:
        if parent is None:
            this = []
        else:
            this = ["    " + parent.render() + " --> " + self.render()]
        children = self.node.render_edge(self)
        return this + children


class DecisionNode(BaseModel):
    decisions: list[Decision]
    desc: str = ""
    id: str = Field(default_factory=guid)

    def render(self) -> str:
        return self.id + "{ }"

    def render_edge(self, parent) -> list[str]:
        if parent is None:
            this = []
        else:
            this = ["    " + parent.render() + " --> " + self.render()]
        children = list(itertools.chain(*[
            node.render_edge(self) for node in self.decisions
        ]))
        return this + children


class DecisionTree(BaseModel):
    root: DecisionNode | ChanceNode
    id: str = Field(default_factory=guid)

    def solve(self) -> tuple[list[Decision], float]:
        return ([], 0.0)

    def render_tree(self) -> str:
        children = self.root.render_edge(None)
        return "flowchart LR\n" + "\n".join(children)

    def write_jpg(self, outfile):
        graph = self.render_tree()
        graphbytes = graph.encode("ascii")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        outbytes = requests.get("https://mermaid.ink/img/" + base64_string).content
        with open(outfile, 'wb') as f:
            f.write(outbytes)

    def html_img_tag(self):
        graph = self.render_tree()
        graphbytes = graph.encode("ascii")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        outbytes = requests.get("https://mermaid.ink/img/" + base64_string).content
        base64_outbytes = base64.b64encode(outbytes)
        base64_string = base64_outbytes.decode("ascii")
        return f"<img src='data:image/jpeg;base64,{base64_string}' alt='tree' style='width:100%' />"


