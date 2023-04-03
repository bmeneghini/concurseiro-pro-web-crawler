import com.amazonaws.services.s3.AmazonS3ClientBuilder
import com.amazonaws.services.s3.model.ObjectMetadata
import com.amazonaws.services.s3.model.PutObjectRequest
import okhttp3.OkHttpClient
import okhttp3.Request
import org.jsoup.Jsoup
import java.io.InputStream

fun main() {
    val url = "https://example.com"
    val htmlContent = getHtmlContent(url)
    val links = extractLinks(htmlContent)
    val pdfLinks = filterPdfLinks(links)
    downloadPdfFiles(pdfLinks)
}

fun getHtmlContent(url: String): String {
    val client = OkHttpClient()
    val request = Request.Builder().url(url).build()
    val response = client.newCall(request).execute()
    return response.body?.string() ?: throw Exception("Failed to get HTML content from $url")
}

fun extractLinks(htmlContent: String): List<String> {
    val doc = Jsoup.parse(htmlContent)
    val linkElements = doc.select("a[href]")
    val links = mutableListOf<String>()
    for (link in linkElements) {
        links.add(link.attr("abs:href"))
    }
    return links
}

fun filterPdfLinks(links: List<String>): List<String> {
    val pdfLinks = mutableListOf<String>()
    for (link in links) {
        if (link.endsWith(".pdf")) {
            pdfLinks.add(link)
        }
    }
    return pdfLinks
}

fun downloadPdfFiles(pdfLinks: List<String>) {
    val s3Client = AmazonS3ClientBuilder.standard().build()
    val bucketName = "cp-nomination-files"
    val existingFiles = s3Client.listObjects(bucketName).objectSummaries.map { it.key }

    val client = OkHttpClient()
    for (link in pdfLinks) {
        val filename = link.substring(link.lastIndexOf("/") + 1)
        if (existingFiles.contains(filename)) {
            println("File $filename already exists in S3, skipping download.")
            continue
        }
        val request = Request.Builder().url(link).build()
        val response = client.newCall(request).execute()

        val inputStream: InputStream = response.body!!.byteStream()
        val metadata = ObjectMetadata().apply { contentLength = response.body!!.contentLength() }
        val requestS3 = PutObjectRequest(bucketName, filename, inputStream, metadata)
        s3Client.putObject(requestS3)

        println("Downloaded and uploaded file: $filename")
    }
}
