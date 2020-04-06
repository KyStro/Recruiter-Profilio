import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

public class FinalExamples {

    public static void main(String[] params) {
        int[] nums = { 3, 7, 5, 12, 20, 15 };
        Node root = new Node(10);
        Node less = new Node(3);
        Node more = new Node(15);
        root.left = less;
        root.right = more;
        less.left = new Node(1);
        more.right = new Node(20);
        more.left = new Node(12);
        /*
         * for (int num : nums) {
         * System.out.println(num);
         * root = root.add(num);
         * }
         */
        // inOrder(root);

        // diceRolls(2);
        // getPerms("cat");
        // combinations("banana", 3);
        // System.out.println(frequency("banana", 'a'));
        // printDigits(42);

        Middle test = new Bottom();
        ((Middle) test).method1();

    }

    public static void binaryHelp(int[] nums, int length) {
        if (nums.length == 0) {
            return;
        }
        if (nums.length == 1) {
            System.out.println(Arrays.toString(nums));
        } else {

        }
    }

    private static void binaryCount(int[] nums) {
        int[] counted = new int[nums.length - 1];

    }

    public static void printDigits(int n) {
        int ones = n % 10;
        int tens = n / 10;
        System.out.println(tens * 10);
        System.out.println(ones);
    }

    private static void printDigits(int n, int divsor) {
        System.out.println(n % divsor);
    }

    public static int frequency(String s, char c) {
        if (s.equals("")) {
            return 0;
        } else if (s.charAt(0) == c) {
            return 1 + frequency(s.substring(1), c);
        } else {
            return frequency(s.substring(1), c);
        }
    }


    public static void combinations(String s, int length) {
        Set<String> all = new TreeSet<String>();
        combinations(s, "", all, length);
        for (String comb : all) {
            System.out.println(comb);
        }
    }

    private static void combinations(String s, String chosen, Set<String> all,
            int length) {
        if (length == 0) {
            all.add(chosen); // base case: no choices left
        } else {
            for (int i = 0; i < s.length(); i++) {
                String ch = s.substring(i, i + 1);
                if (!chosen.contains(ch)) {
                    String rest = s.substring(0, i) + s.substring(i + 1);
                    combinations(rest, chosen + ch, all, length - 1);
                }
            }
        }
    }


    public static void getPerms(String s) {
        String result = "";
        String soFar = "";
        getPerms(s, soFar, result);
    }

    private static void getPerms(String s, String soFar, String result) {
        if (s.length() == soFar.length()) {
            System.out.println(soFar);
        } else {
            for (int i = 0; i < s.length(); i++) {
                String choose = s.substring(i + i + 1);
                getPerms(s.substring(i + 1), soFar + choose, result);
                soFar = soFar.substring(0, result.length() - 2);
            }
        }
    }

    public static void diceRolls(int dice) {
        // collection init in main method
        List<Integer> chosen = new ArrayList<Integer>();
        // helper is then called
        diceRolls(dice, chosen);
    }

    // private recursive helper to implement diceRolls logic
    private static void diceRolls(int dice, List<Integer> chosen) {
        if (dice == 0) {
            System.out.println(chosen); // base case
        } else {
            for (int i = 1; i <= 6; i++) {
                // first dice is chosen
                chosen.add(i); // choose
                System.out.println(i + " is chosen");
                // one less dice to choose, recursive call
                diceRolls(dice - 1, chosen); // explore
                // remove last chosen from collection
                chosen.remove(chosen.size() - 1); // un-choose
            }
            System.out.println();
        }
    }

    private static void inOrder(Node node) {
        if (node == null) {
            return;
        }
        inOrder(node.left);
        System.out.print(node.value + " ");
        inOrder(node.right);
    }

}