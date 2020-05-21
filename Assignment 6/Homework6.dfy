datatype Tree<T> = Leaf | Node(Tree<T>, Tree<T>, T)
datatype List<T> = Nil | Cons(T, List<T>)

function flatten<T>(tree:Tree<T>):List<T>
{
        match tree
        case Leaf => Nil
        case Node(leftTree, rightTree, x) => Cons(x, append(flatten(leftTree), flatten(rightTree)))
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


lemma appendListContains<T>(xs:List<T>, ys:List<T>, element:T)
ensures listContains(append(xs, ys), element) <==> listContains(xs, element) || listContains(ys, element) 
{
        match xs
        case Nil => {}
        case Cons(x, xs') => {}
}

lemma sameElements<T>(tree:Tree<T>, element:T)
ensures treeContains(tree, element) <==> listContains(flatten(tree), element)
{
	match tree
        case Leaf => {}
        case Node(leftTree, rightTree, x) => {
            sameElements(leftTree, x);
            sameElements(rightTree, x);
            appendListContains(flatten(leftTree), flatten(rightTree), element);

            calc { treeContains(tree, element);
                == treeContains(Node(leftTree, rightTree, x), element);
                == treeContains(leftTree, element) || treeContains(rightTree, element) || x == element;
                == listContains(flatten(leftTree), element) || listContains(flatten(rightTree), element) || x == element;
                == listContains(flatten(leftTree), element) || listContains(Cons(x, flatten(rightTree)), element);
                == listContains(append(Cons(x, flatten(leftTree)), flatten(rightTree)), element);
                == listContains(Cons(x, append(flatten(leftTree), flatten(rightTree))), element);
                == listContains(flatten(tree), element);
            }
        }
}