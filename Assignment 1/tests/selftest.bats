load harness

@test "mytest-1" {
  check '-1 * 0 * 10' '0'
}

@test "mytest-2" {
  check '3 * -3 + 10 - 6 * -2' '13'
}

@test "mytest-3" {
  check '-5 * -5 + 5 * 5' '50'
}

@test "mytest-4" {
  check '-0 * 0 - 0 * -0' '0'
}

@test "mytest-5" {
  check '-2 * -2 - 2' '2'
}
