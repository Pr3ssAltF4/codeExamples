import java.text.DecimalFormat;

/**
 * Created by Ian on 2/20/2015.
 */
public abstract class BankAccount {

    private double balance;
    private String name;
    private double interest;
    DecimalFormat df = new DecimalFormat("#.##"); // Used to round to 100th's place

    // Ctor
    public BankAccount (double newMoney, String ownerName) {
        this.balance = newMoney;
        this.name = ownerName;
    }

    // adds the interest to the account
    protected void addInterest(double newInterestEarned) {
        balance += newInterestEarned;
        interest = newInterestEarned;
    }

    // calculates the interest, deferred to be defined in other sub classes
    abstract void calcInterest();

    // returns the 2 character moniker for the account type
    abstract String getAccountType();

    // returns the current balance of the account
    public double getCurrentBalance() { return balance; }

    // returns the most recent amount of interest earned
    public double getInterest() { return interest; }

    // prints the monthly statement for the account
    public void printStatement() {
        System.out.println(this.toString());

    }

    // adds the interest to the current balance and sets the interest
    protected void setInterestEarned(double interest) {
        balance += interest;
        balance = Double.parseDouble(df.format(balance));
        this.interest = Double.parseDouble(df.format(interest));
    }

    // ...
    public String toString() {
        return getAccountType() + "   " + name + "     Interest Earned:     " + interest +
                "     Current Balance:      " + balance;
    }




}
