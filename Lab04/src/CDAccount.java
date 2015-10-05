/**
 * Created by Ian on 2/20/2015.
 */
public class CDAccount extends BankAccount {

    private String CD_ACCOUNT = "CD";
    private static double MINIMUM_BALANCE = 1000;
    private static double MONTHLY_INTEREST_RATE = 0.06;

    public CDAccount(double newMoney, String owner) {
        super (newMoney, owner);
    }

    public void calcInterest() {
        if(super.getCurrentBalance() > MINIMUM_BALANCE)
            super.setInterestEarned(super.getCurrentBalance() * MONTHLY_INTEREST_RATE);
    }

    public String getAccountType() { return CD_ACCOUNT; }

    public String toString() {
        return super.toString();
    }

}
