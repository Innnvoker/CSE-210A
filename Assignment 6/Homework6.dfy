datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)

function flatten<T>(tree:Tree<T>):List<T>
{
    match tree
    case Leaf => Nil
    case Node(leftTree, rightTree, x) => append(flatten(leftTree), Cons(x, flatten(rightTree)))
}

function append<T>(xs:List<T>, ys:List<T>):List<T>
{
    match xs
    case Nil => ys
    case Cons(x, xs') => Cons(x, append(xs', ys))
}

function treeContains<T>(tree:Tree<T>, element:T):bool
{
	match tree
    case Leaf => false
    case Node(leftTree, rightTree, x) => treeContains(leftTree, element) || treeContains(rightTree, element) || x == element
}

function listContains<T>(xs:List<T>, element:T):bool
{
	match xs
    case Nil => false
    case Cons(x, xs') => listContains(xs', element) || x == element
}


lemma sameElements<T>(tree:Tree<T>, element:T)
ensures treeContains(tree, element) <==> listContains(flatten(tree), element)
{
	match tree
    case Leaf => {}
    case Node(leftTree, rightTree, x) => {
        sameElements(leftTree, x);
        sameElements(rightTree, x);

        assert treeContains(tree, element)
            == (treeContains(leftTree, element) || treeContains(rightTree, element) || x == element)
            == (listContains(flatten(leftTree), element) || listContains(flatten(rightTree), element) || x == element)
            == (listContains(flatten(leftTree), element) || (listContains(Cons(x, flatten(rightTree)), element)))
            == listContains(append(flatten(leftTree), Cons(x, flatten(rightTree))), element)
            == listContains(flatten(tree), element);
    
        assert listContains(flatten(tree), element)
            == listContains(append(flatten(leftTree), Cons(x, flatten(rightTree))), element)
            == (listContains(flatten(leftTree), element) || listContains(Cons(x, flatten(rightTree)), element))
            == (listContains(flatten(leftTree), element) || listContains(flatten(rightTree), element) || x == element)
            == (treeContains(leftTree, element) || treeContains(rightTree, element) || x == element)
            == treeContains(tree, element);
    }
}