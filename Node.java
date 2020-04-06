

public class Node {

    public Node left;
    public Node right;
    public int value;

    public Node(int val) {

    this.value = val;
        this.left = null;
        this.right = null;

    }

    public Node add(int newVal) {
        Node newNode = new Node(newVal);
        if (newNode.value < this.value && this.left == null) {
            this.left = newNode;
            return this;
        }
        if (newNode.value > this.value && this.right == null) {
            this.right = newNode;
            return this;

        } else {
            this.left.add(newVal);
            this.right.add(newVal);

        }
        return this;

        // make new node
        // check if want to add new node to left or right
        // when you know check left or right to see if node is there
        // if node isnt there you add there
        // if it is there you recurse call on node thats there

    }

    private boolean nodeNull(Node node) {
        return node == null;
    }

    /*
     * private Node goThru(Node parent, Node newNode) {
     * if (parent == null) {
     * return newNode;
     * } else if (newNode.value < parent.value) {
     * parent.left = this.goThru(parent.left, newNode);
     * } else if (newNode.value > parent.value) {
     * parent.right = this.goThru(parent.right, newNode);
     * }
     * return parent;
     * }
     */

    public void print() {
        if (this == null) {
            return;
        }

        this.left.print();
        System.out.println((this.value));
        this.right.print();

    }

}
