load harness

@test "new-1" {
  check 'z := 26 ; y := 1 ; x := 2' '⇒ skip; y := 1; x := 2, {z → 26}
⇒ y := 1; x := 2, {z → 26}
⇒ skip; x := 2, {y → 1, z → 26}
⇒ x := 2, {y → 1, z → 26}
⇒ skip, {x → 2, y → 1, z → 26}'
}

@test "new-2" {
  check 'if y = 0 ∨ x < 4 then x := 1 else x := 3' '⇒ x := 1, {}
⇒ skip, {x → 1}'
}

@test "new-3" {
  check 'x := 1 * 9 ; if 5 < x then x := 2 - 2 else y := 9' '⇒ skip; if (5<x) then { x := (2-2) } else { y := 9 }, {x → 9}
⇒ if (5<x) then { x := (2-2) } else { y := 9 }, {x → 9}
⇒ x := (2-2), {x → 9}
⇒ skip, {x → 0}'
}

@test "new-4" {
  check 'fact := 100' '⇒ skip, {fact → 100}'
}

@test "new-5" {
  check 'if false then x := 1 else x := 0' '⇒ x := 0, {}
⇒ skip, {x → 0}'
}