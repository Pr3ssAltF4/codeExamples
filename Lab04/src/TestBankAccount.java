import java.text.DecimalFormat;
import java.util.ArrayList;

/**
 * Created by Ian on 2/23/2015.
 */
public class TestBankAccount {

    public static void main (String [] args) {
        ArrayList<BankAccount> testArrList = new ArrayList<BankAccount>();
        BankAccount test01 = new CDAccount(100, "Ian Taylor");
        BankAccount test02 = new SavingsAccount(999, "Izzy Taylor");
        BankAccount test03 = new CheckingAccount(50, "A Newb", true);
        BankAccount test04 = new CheckingAccount(501, "Oscar Herrera", true);
        BankAccount test05 = new SavingsAccount(1001, "Adam Taylor");
        testArrList.add(test01);
        testArrList.add(test02);
        testArrList.add(test03);
        testArrList.add(test04);
        testArrList.add(test05);
        DecimalFormat df = new DecimalFormat("#.##");
        double totalInterestEarned = 0;
        double totalBalance = 0;
        int i = 1;

        for (i = 1; i < 5; i++) {
            System.out.println("\nMonthly Statement " + i + "\n");
            for (BankAccount e : testArrList) {
                e.calcInterest();
                totalInterestEarned += e.getInterest();
                totalBalance += e.getCurrentBalance();
                e.printStatement();
            }
        } System.out.println("\nTotal Interest: " + df.format(totalInterestEarned) + "\nTotal Balance: " + df.format(totalBalance));
    }

}
