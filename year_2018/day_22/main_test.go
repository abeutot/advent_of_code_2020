package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestAll(t *testing.T) {
	assert.Equal(t, 0, geologicIndex(0, 0))
	assert.Equal(t, 510, erosionLevel(0, 0))
	assert.Equal(t, ROCKY, type_(0, 0))

	assert.Equal(t, 16807, geologicIndex(1, 0))
	assert.Equal(t, 17317, erosionLevel(1, 0))
	assert.Equal(t, WET, type_(1, 0))

	assert.Equal(t, 48271, geologicIndex(0, 1))
	assert.Equal(t, 8415, erosionLevel(0, 1))
	assert.Equal(t, ROCKY, type_(0, 1))

	assert.Equal(t, 145722555, geologicIndex(1, 1))
	assert.Equal(t, 1805, erosionLevel(1, 1))
	assert.Equal(t, NARROW, type_(1, 1))

	assert.Equal(t, 0, geologicIndex(10, 10))
	assert.Equal(t, 510, erosionLevel(10, 10))
	assert.Equal(t, ROCKY, type_(10, 10))
}
