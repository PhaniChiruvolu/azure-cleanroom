// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using Controllers;

namespace CcfProviderClient;

public class Program
{
    public static void Main(string[] args)
    {
        ApiMain.Main(args, builder => new Startup(builder.Configuration));
    }
}
