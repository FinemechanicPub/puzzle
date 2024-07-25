import { expect, test } from "vitest";
import divmod from "./divmod";

test("divmod(4, 2) -> 2, 0", () => expect(divmod(4, 2)).toEqual([2, 0]))
test("divmod(4, 3) -> 1, 1", () => expect(divmod(4, 3)).toEqual([1, 1]))
