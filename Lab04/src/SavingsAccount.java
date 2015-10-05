/**
 * Created by Ian on 2/20/2015.
 */
public class SavingsAccount extends BankAccount {

    private String SAVINGS_ACCOUNT = "SA";
    private static double SAVINGS_MONTHLY_INTEREST_RATE = 0.03;

    public SavingsAccount(double newMoney, String owner) {
        super(newMoney, owner);
    }

    public void calcInterest() {  super.setInterestEarned(SAVINGS_MONTHLY_INTEREST_RATE * super.getCurrentBalance()); }

    public String getAccountType() { return SAVINGS_ACCOUNT; }

    public String toString() { return super.toString(); }
}
