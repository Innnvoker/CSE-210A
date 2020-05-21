datatype Exp = Const(int) | Var(string) | Plus(Exp, Exp) |  Mult(Exp, Exp)

function eval(e:Exp, store:map<string, int>):int
{
	match(e)
		case Const(n) => n
		case Var(s) => if(s in store) then store[s] else -1
		case Plus(e1, e2) => eval(e1, store) + eval(e2, store)
		case Mult(e1, e2) => eval(e1, store) * eval(e2, store)
}

//fill this function in to make optimizeFeatures work
function optimize(e:Exp):Exp
{
	match e
	case Const(n) => Const(n)
	case Var(s) => Var(s)
	case Plus(e1, e2) => 
		var e1' := optimize(e1);
		var e2' := optimize(e2);
		match (e1', e2') {
			case(Const(a), Const(b)) => Const(a + b)
			case(Const(a), Var(y)) => if a == 0 then Var(y) else Plus(e1', e2')
			case(Const(a), Plus(x', y')) => if a == 0 then Plus(x', y') else Plus(e1', e2')
			case(Const(a), Mult(x', y')) => if a == 0 then Mult(x', y') else Plus(e1', e2')

			case(Var(x), Const(b)) => if b == 0 then Var(x) else Plus(e1', e2')
			case(Var(x), Var(y)) => Plus(e1', e2')
			case(Var(x), Plus(x', y')) => Plus(e1', e2')
			case(Var(x), Mult(x', y')) => Plus(e1', e2')
			
			case(Plus(x', y'), Const(b)) => if b == 0 then Plus(x', y') else Plus(e1', e2')
			case(Plus(x', y'), Var(y)) => Plus(e1', e2')
			case(Plus(x', y'), Plus(m', n')) => Plus(e1', e2')
			case(Plus(x', y'), Mult(m', n')) => Plus(e1', e2')

			case(Mult(x', y'), Const(b)) => if b == 0 then Mult(x', y') else Plus(e1', e2')
			case(Mult(x', y'), Var(y)) => Plus(e1', e2')
			case(Mult(x', y'), Plus(m', n')) => Plus(e1', e2')
			case(Mult(x', y'), Mult(m', n')) => Plus(e1', e2')
		}
	case Mult(e1, e2) => 
		var e1' := optimize(e1);
		var e2' := optimize(e2);
		match (e1', e2') {
			case(Const(a), Const(b)) => Const(a * b)
			case(Const(a), Var(y)) => if a == 0 then Const(0) else Mult(e1', e2')
			case(Const(a), Plus(x', y')) => if a == 0 then Const(0) else Mult(e1', e2')
			case(Const(a), Mult(x', y')) => if a == 0 then Const(0) else Mult(e1', e2')

			case(Var(x), Const(b)) => if b == 0 then Const(0) else Mult(e1', e2')
			case(Var(x), Var(y)) => Mult(e1', e2')
			case(Var(x), Plus(x', y')) => Mult(e1', e2')
			case(Var(x), Mult(x', y')) => Mult(e1', e2')
			
			case(Plus(x', y'), Const(b)) => if b == 0 then Const(0) else Mult(e1', e2')
			case(Plus(x', y'), Var(y)) => Mult(e1', e2')
			case(Plus(x', y'), Plus(m', n')) => Mult(e1', e2')
			case(Plus(x', y'), Mult(m', n')) => Mult(e1', e2')

			case(Mult(x', y'), Const(b)) => if b == 0 then Const(0) else Mult(e1', e2')
			case(Mult(x', y'), Var(y)) => Mult(e1', e2')
			case(Mult(x', y'), Plus(m', n')) => Mult(e1', e2')
			case(Mult(x', y'), Mult(m', n')) => Mult(e1', e2')
		}
}

//as you write optimize this will become unproved
//you must write proof code so that Dafny can prove this
method optimizeCorrect(e:Exp, s:map<string, int>)
ensures eval(e,s) == eval(optimize(e), s)
{
	match e
	case Const(n) => {}
	case Var(s) => {}
	case Plus(e1, e2) => {
		optimizeCorrect(e1, s);
		optimizeCorrect(e2, s);


	}
	case Mult(e1, e2) => {
		optimizeCorrect(e1, s);
		optimizeCorrect(e2, s);

	}
}

method optimizeFeatures()
{

	assert( optimize(Mult(Var("x"), Const(0))) == Const(0) );
	assert( optimize(Mult(Var("x"), Const(1))) == Var("x") );
	assert( optimize(Mult(Const(0), Var("x"))) == Const(0) );
	assert( optimize(Mult(Const(1), Var("x"))) == Var("x") );

	assert( optimize(Plus(Const(0), Var("x"))) == Var("x") );
	assert( optimize(Plus(Var("x"), Const(0))) == Var("x") );

	assert( optimize(Plus(Const(3),Const(4))) == Const(7) );
	assert( optimize(Mult(Const(3),Const(4))) == Const(12) );


	assert( optimize(Plus(Plus(Var("x"), Var("y")), Const(0))) == Plus(Var("x"), Var("y")) );
	
}