from __future__ import annotations
import bentoml


EXAMPLE_INPUT = "Breaking News: In an astonishing turn of events, the small town of Willow Creek has been taken by storm as local resident Jerry Thompson's cat, Whiskers, performed what witnesses are calling a 'miraculous and gravity-defying leap.' Eyewitnesses report that Whiskers, an otherwise unremarkable tabby cat, jumped a record-breaking 20 feet into the air to catch a fly. The event, which took place in Thompson's backyard, is now being investigated by scientists for potential breaches in the laws of physics. Local authorities are considering a town festival to celebrate what is being hailed as 'The Leap of the Century."


@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
)
class Tabby:
    def __init__(self) -> None:
        pass

    @bentoml.api
    def completion(self, text: str = EXAMPLE_INPUT) -> str:
        return "hello world"