import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class TranslateClient {

    private static final String URL_SERVER = "https://translate_dev.abcpen.com";
    // private static final String URL_SERVER = "http://127.0.0.1:3701";
    // private static final String URL_SERVER = "http://192.168.10.2:3701";
    // private static final String URL_SERVER = "https://translate_v2.abcpen.com";

    private static final String application_key = "test1";
    private static final String application_secret = "2258ACC4-199B-4DCB-B6F3-C2485C63E85A";

    private static String generateSignature(String appId, String apiKey) throws NoSuchAlgorithmException, InvalidKeyException {
        long timestamp = System.currentTimeMillis() / 1000L;
        String baseString = appId + timestamp;

        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] messageDigest = md.digest(baseString.getBytes(StandardCharsets.UTF_8));
        String base64 = Base64.getEncoder().encodeToString(messageDigest);

        javax.crypto.spec.SecretKeySpec keySpec = new javax.crypto.spec.SecretKeySpec(apiKey.getBytes(StandardCharsets.UTF_8), "HmacSHA1");
        javax.crypto.Mac mac = javax.crypto.Mac.getInstance("HmacSHA1");
        mac.init(keySpec);

        byte[] result = mac.doFinal(base64.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(result);
    }

    private static void translateSentence(String sentence, String sourceLang, String targetLang) throws IOException, InterruptedException {
        String endpoint = "/v1/translate/sentence";
        String expectedSignature = generateSignature(application_key, application_secret);
        String timestamp = String.valueOf(System.currentTimeMillis() / 1000L);

        Map<Object, Object> values = new HashMap<>();
        values.put("sentence", java.util.Base64.getEncoder().encodeToString(sentence.getBytes(StandardCharsets.UTF_8)));
        values.put("source_lang", sourceLang);
        values.put("target_lang", targetLang);

        String url = URL_SERVER + endpoint;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Content-Type", "application/json")
                .header("X-App-Key", application_key)
                .header("X-App-Signature", expectedSignature)
                .header("X-Timestamp", timestamp)
                .POST(buildFormDataFromMap(values))
                .build();

        HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("translateSentence, Result: " + response.body());
    }

    private static HttpRequest.BodyPublisher buildFormDataFromMap(Map<Object, Object> data) {
        var builder = new StringBuilder();
        for (Map.Entry<Object, Object> entry : data.entrySet()) {
            if (builder.length() > 0) {
                builder.append("&");
            }
            builder.append(URLEncoder.encode(entry.getKey().toString(), StandardCharsets.UTF_8));
            builder.append("=");
            builder.append(URLEncoder.encode(entry.getValue().toString(), StandardCharsets.UTF_8));
        }
        return HttpRequest.BodyPublishers.ofString(builder.toString());
    }

    public static void main(String[] args) {
        try {
            translateSentence("这是一个测试句子", "zh", "en");
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
