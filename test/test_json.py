__all__ = ["JSONTestCase"]
import os
import sys
import asyncio
import unittest
import pygada_runtime


TEST_JSON = os.path.join(os.path.dirname(__file__), "data", "test.json")


class JSONTestCase(unittest.TestCase):
    def test(self):
        async def work():
            """This node has an implicit configured module."""
            r, w = os.pipe()
            w = os.fdopen(w, "w")
            proc = await pygada_runtime.run(
                ["lang.json", "--input", TEST_JSON, "--chain-output"], stdout=w
            )
            await proc.wait()
            w.close()
            r = os.fdopen(r)
            s = r.read()
            r.close()
            proc = await pygada_runtime.run(
                ["lang.json", "--input", TEST_JSON, "--output", f"{TEST_JSON}2"]
            )
            await proc.wait()

        asyncio.run(work())


if __name__ == "__main__":
    unittest.main()
