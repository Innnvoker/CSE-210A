package myPackage;
import java.util.Scanner;
import java.util.StringTokenizer;
//import myPackage.MathTokenize;
//import myPackage.NotationConverter;
//import myPackage.SyntaxTree;

public class assignmentOne{

    public static void main(String [] args) {
        Scanner scan = new Scanner(System.in);
        while (scan.hasNextLine()) {
            String line = scan.nextLine();
            //StringTokenizer str = new StringTokenizer(line);
            String[] input = line.split(operator.space);

            BinaryTree tree = new BinaryTree();




//            while (str.hasMoreElements()) {
//                String curr = str.nextToken();
//                if (curr.equals(operator.plus)) {
//                    System.out.println(curr);
//                }
//
//            }
//            System.out.println(line.charAt(2));

        }
        scan.close();
    }

    public static class operator {
        public static String space = " ";
        public static String plus = "+";
        public static String minus = "-";
        public static String multi = "*";
        public static String div = "/";
        public static String leftPar = "(";
        public static String rightPar = ")";
    }
}



class Node {
    String key;
    int val;
    Node left, right;
    public Node(String item, int num) {
        key = item;
        val = num;
        left = right = null;
    }
}

class BinaryTree {
    Node root;
    BinaryTree(String key, int num) {
        root = new Node(key, num);
    }
    BinaryTree() {
        root = null;
    }
}
//
//public int postOrder(Node curr) {
//    int res = 0;
//    if (curr != null) {
//        postOrder(curr.left);
//        postOrder(curr.right);
//    }
//}


