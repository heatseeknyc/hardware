require 'net/http'
require 'json'

on = true

while on do

  sofar = open('sofar.txt', 'r')
  current_reading = sofar.read.to_i
  sofar.close

  readings = open('readings.tsv', 'r').readlines
  readings = readings.slice(current_reading..-2) # don't include last line, in case it is unfinished
  uri = URI('http://heatseeknyc.com/readings.json')

  readings.each do |reading|
    reading = reading.chop
    time, sensor_name, temp, verification = reading.split("\t")

    req = Net::HTTP::Post.new(uri, initheader = {'Content-Type' =>'application/json'})
    req.body = {reading: {sensor_name: sensor_name, temp: temp, time: time, verification: verification}}.to_json
    res = Net::HTTP.start('heatseeknyc.com', 80) do |http|
      response = http.request(req)
      puts "Reading sent, response code = #{response.code}"
      
      current_reading +=1 if response.code == "200"
    end

    sleep(2)

  end

  sofar = open('sofar.txt', 'w')
  sofar.puts(current_reading)
  sofar.close

  # sleep(600)

  on = false

end


# curl -X POST -H "Content-Type: application/json" -d '{"reading": {"sensor_name": "tahiti", "temp": "56", "time": "Wed Jul  2 16:07:09 EDT 2014", "verification": "1234"}}' http://heatseeknyc.com/readings.json



