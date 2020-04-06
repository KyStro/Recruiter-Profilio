
public class Recursion {

    public static void main(String[] args) {
        printTriangle(6);
    }

    public static String printTriangle(int count) {
        if (count <= 0)
            return "";

        String p = helper(count / 2, count) + printTriangle(count - 2);
        System.out.println(p);

        return p;
    }

    public static String helper(int n, int real) {
        String s = "";
        int spaces = (real - n);
        for (int i = 0; i <= spaces; i++) {
            s += " ";
        }
        s += "*";
        return s;
    }

    public static void iteration(int n) {
        int t = 0;
        String s = "";
        for (int i = 0; i <= n; i += 2) {
            t += 1;
            s += " ";

        }
        s += "*";
        System.out.println();
    }

}
