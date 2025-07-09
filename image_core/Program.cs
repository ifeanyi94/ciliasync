using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Processing;
using Newtonsoft.Json;
using System.Text.Json.Serialization;

if (args.Length < 2)
{
    Console.WriteLine("Usage: dotnet run <input_image> <output_json>");
    return;
}

string inputPath = args[0];
string outputPath = args[1];

if (!File.Exists(inputPath))
{
    Console.WriteLine("Error: File not found - " + inputPath);
    return;
}

// Load and process image
using Image<Rgba32> image = Image.Load<Rgba32>(inputPath);
image.Mutate(x => x.Grayscale()); // Apply grayscale

int membraneArea = 0;

// Count non-black pixels (simulate edge/mask)
for (int y = 0; y < image.Height; y++)
{
    for (int x = 0; x < image.Width; x++)
    {
        Rgba32 pixel = image[x, y];
        if (pixel.R > 30) // Threshold for "bright enough"
            membraneArea++;
    }
}

double colocPercent = 0.84; // Simulated for now

var result = new
{
    membrane_area = membraneArea,
    coloc_percent = colocPercent
};

string json = JsonConvert.SerializeObject(result, Formatting.Indented);
File.WriteAllText(outputPath, json);

Console.WriteLine("Analysis complete. JSON saved to: " + outputPath);
