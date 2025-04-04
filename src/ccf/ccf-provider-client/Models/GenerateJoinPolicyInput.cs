﻿// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

namespace Controllers;

public class GenerateJoinPolicyInput
{
    public string InfraType { get; set; } = default!;

    public string? SecurityPolicyCreationOption { get; set; } = default!;
}