
import { AssignDriverColours } from './UnitTestFunc.mjs';
//Unit tests
test("Check if colours returns values", () => {
  expect(AssignDriverColours()).not.toBeUndefined()
});