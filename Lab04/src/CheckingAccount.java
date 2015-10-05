/**
 * Created by Ian on 2/20/2015.
 */
public class CheckingAccount extends BankAccount {

    private static double BONUS_MONTHLY_RATE = 0.001;
    private String CHECKING_ACCOUNT;
    private static double PREMIUM_CHECKING_MINIMUM_BALANCE = 500;
    private boolean bonus;

    public CheckingAccount(double newMoney, String owner, boolean bonus) {
        super(newMoney, owner);
        if(bonus) CHECKING_ACCOUNT = "CI";
        else CHECKING_ACCOUNT = "CN";
        this.bonus = bonus;
    }

    public void calcInterest() { if(bonus && super.getCurrentBalance() > PREMIUM_CHECKING_MINIMUM_BALANCE) super.setInterestEarned(BONUS_MONTHLY_RATE * super.getCurrentBalance()); }

    public String getAccountType() { return CHECKING_ACCOUNT; }

    public String toString () { return super.toString(); }

}
