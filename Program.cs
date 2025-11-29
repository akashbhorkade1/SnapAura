using System.Drawing;
using System.Drawing.Imaging;

namespace SnapAura;

internal class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("SnapAura Worker started.");

        string inputPath = "input.jpg";   // Put a test image here
        string outputPath = "output.jpg";

        if (!File.Exists(inputPath))
        {
            Console.WriteLine("No input image found.");
            return;
        }

        using var image = new Bitmap(inputPath);

        // Simple enhancement: sharpen + upscale
        var enhanced = EnhanceImage(image);

        enhanced.Save(outputPath, ImageFormat.Jpeg);
        Console.WriteLine($"Enhanced image saved to {outputPath}");
    }

    static Bitmap EnhanceImage(Bitmap original)
    {
        int newWidth = original.Width * 2;
        int newHeight = original.Height * 2;
        var resized = new Bitmap(original, newWidth, newHeight);

        // Apply basic sharpening (simulated)
        using var g = Graphics.FromImage(resized);
        g.DrawImage(resized, 0, 0);

        return resized;
    }
}

