import { expect, test } from "vitest";
import counter from "./counter";

const samples = [
    [{id: 1}, {id: 3}, {id: 2}, {id: 3}],
    []
]

const expected = [
    {1:1, 3:2, 2:1},
    {}
]

for (const [index, sample] of samples.entries()){
    test("counter", () => expect(counter(sample)).toEqual(expected[index]))
}