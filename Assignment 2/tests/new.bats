load harness

@test "new-1" {
  check 'true ? y := 1 : z := 1' '{y → 1}'
}

@test "new-2" {
  check 'false ? y := 1 : z := 1' '{z → 1}'
}

@test "new-3" {
  check 'true ? y := 1 : z := 1 ; false ? y := 1 : z := 1' '{y → 1, z → 1}'
}

@test "new-4" {
  check 'false ? y := 1 : z := 2 ; false ? y := 1 : z := 1' '{z → 1}'
}

@test "new-5" {
  check 'a := 5 ; b := 10 ; a < b ? a := a - 1 : b := b - 1' '{a → 4, b → 10}'
}