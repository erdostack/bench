<?php

namespace App\Http\Controllers;

use App\Repositories\PartRepository;

class PartController extends Controller
{
    public function show(int $partId, PartRepository $parts)
    {
        $part = $parts->find($partId);
        abort_if($part === null, 404);

        $replacements = $part->orderable ? [] : $parts->currentReplacements($partId);

        return view('parts.show', compact('part', 'replacements'));
    }
}
