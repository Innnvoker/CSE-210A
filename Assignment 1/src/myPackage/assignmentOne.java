package myPackage;
import java.util.Arrays;
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
            String[] input = line.split(operator.space);
            AST ast = new AST();
            assignmentOne ass = new assignmentOne();
            ast.root = ass.parseString(input);

            System.out.println(ast.root.left.val);
            System.out.println(ast.root.left.key);

            System.out.println(ast.root.val);
            System.out.println(ast.root.key);

            System.out.println(ast.root.right.val);
            System.out.println(ast.root.right.key);

//            int res = ass.calculate(ast.root);
//            System.out.println(res);
//            ass.printTree(ast.root);

            //StringTokenizer str = new StringTokenizer(line);

//            while (str.hasMoreElements()) {
//                String curr = str.nextToken();
//                if (curr.equals(operator.plus)) {
//                    System.out.println(curr);
//                }
//            }
        }
        scan.close();
    }


    public Node parseString(String[] input) {
        Node newNode = new Node();
        if (input.length == 1) {
            newNode.val = Integer.parseInt(input[0]);
            return newNode;
        }
        for (int i = 0; i < input.length; i++) {
            String str = input[i];
            if (str.equals(operator.plus) || str.equals(operator.subtr)) {
                newNode.key = str;
                newNode.val = 0;
                String[] leftStr = Arrays.copyOfRange(input, 0, i);
                String[] rightStr = Arrays.copyOfRange(input, i+1, input.length);

//                System.out.println(Arrays.toString(leftStr));
//                System.out.println(Arrays.toString(rightStr));

                if (leftStr.length > 0) {
                    newNode.left = parseString(leftStr);
                }
                if (rightStr.length > 0) {
                    newNode.right = parseString(rightStr);
                }
            }
            else if (str.equals(operator.multi) || str.equals(operator.divide)) {
                newNode.key = str;
                newNode.val = 0;
                String[] leftStr = Arrays.copyOfRange(input, 0, i);
                String[] rightStr = Arrays.copyOfRange(input, i+1, input.length);
                if (leftStr.length > 0) {
                    newNode.left = parseString(leftStr);
                }
                if (rightStr.length > 0) {
                    newNode.right = parseString(rightStr);
                }
            }
        }
        return newNode;
    }

    public int calculate(Node currNode) {
        if (currNode.key == null) {
            System.out.println(currNode.val);
            return currNode.val;
        }
        if (currNode.key.equals(operator.plus)) {
            System.out.println("+");
            currNode.val = calculate(currNode.left) + calculate(currNode.right);
            return currNode.val;
        }
        else if (currNode.key.equals(operator.subtr)) {
            currNode.val = calculate(currNode.left) - calculate(currNode.right);
            return currNode.val;
        }
        else if (currNode.key.equals(operator.multi)) {
            System.out.println("*");
            currNode.val = calculate(currNode.left) * calculate(currNode.right);
            return currNode.val;
        }
        else if (currNode.key.equals(operator.divide)) {
            currNode.val = calculate(currNode.left) / calculate(currNode.right);
            return currNode.val;
        }
        return currNode.val;
    }

    public void printTree(Node curr) {
        if (curr != null) {
            printTree(curr.left);
            System.out.println(curr.key);
            System.out.println(curr.val);
            printTree(curr.right);
        }
    }

    public static class operator {
        public static String space = " ";
        public static String plus = "+";
        public static String subtr = "-";
        public static String multi = "*";
        public static String divide = "/";
        public static String leftPar = "(";
        public static String rightPar = ")";
    }



    public int add(Node node) {
        return node.left.val + node.right.val;
    }
    public int minus(Node node) {
        return node.left.val - node.right.val;
    }
    public int mul(Node node) {
        return node.left.val * node.right.val;
    }
    public int div(Node node) {
        return node.left.val / node.right.val;
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
    public Node() {
        key = null;
        val = 0;
        left = right = null;
    }
}

class AST {
    Node root;
    AST(String key, int num) {
        root = new Node(key, num);
    }
    AST() {
        root = null;
    }
}



