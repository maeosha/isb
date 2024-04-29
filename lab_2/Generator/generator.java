import java.util.Random;

public class Main
{
    public static String GetRandomNumbers(int count) {
        /*
         * Generating a pseudorandom bit sequence
         */

        Random random = new Random();
        String random_sequence = "";

        for (int i = 0; i < count; i++) {
            random_sequence += random.nextInt(2);
        }
        return random_sequence;
    }

	public static void main(String[] args) {
		String random_sequence = GetRandomNumbers(128);
		System.out.print(random_sequence);
	}
}