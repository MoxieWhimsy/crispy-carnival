

class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ''
        if self.props is None:
            return result
        for prop in self.props:
            result += f' {prop}="{self.props[prop]}"'
        return result

    def __repr__(self):
        return f'tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}'

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None or self.tag == '':
            return f'{self.value}'

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'tag: {self.tag}, value: {self.value}, props: {self.props}'

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == '':
            raise ValueError("tag is required")
        if self.children is None:
            raise ValueError("children is required")

        result = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            result += child.to_html()

        result += f'</{self.tag}>'
        return result
