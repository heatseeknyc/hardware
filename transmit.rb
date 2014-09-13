require 'net/http'
require 'json'

DATA_DIR = 'data/'
PROGRESS_PATH = DATA_DIR + 'progress'
READINGS_PATH = DATA_DIR + 'readings.tsv'

on = true

while on do

  sofar = open(PROGRESS_PATH)
  current_reading = sofar.read.to_i
  sofar.close

  readings = open(READINGS_PATH).readlines
  readings = readings.slice(current_reading..-2) # don't include last line, in case it is unfinished
  uri = URI('http://heatseeknyc.com/readings.json')

  readings.each do |reading|
    puts reading
    reading = reading.chop
    time, sensor_name, temp, verification = reading.split("\t")

    current_reading +=1
    sofar = open(PROGRESS_PATH, 'w')
    sofar.puts(current_reading)
    sofar.close

    req = Net::HTTP::Post.new(uri, initheader = {'Content-Type' =>'application/json'})
    req.body = {reading: {sensor_name: sensor_name, temp: temp, time: time, verification: verification}}.to_json
    res = Net::HTTP.start('heatseeknyc.com', 80, :open_timeout => 1, :read_timeout => 1) do |http|
      response = http.request(req)
      puts "Reading sent on Demo Day, response code = #{response.code}"
      if response.code != "200"
        puts uri
        puts req.body
        puts response.body
        puts "skipping..."
      end
    end

    sleep(0.1)

  end

  sleep(0.5)

end


# curl -X POST -H "Content-Type: application/json" -d '{"reading": {"sensor_name": "tahiti", "temp": "56", "time": "Wed Jul  2 16:07:09 EDT 2014", "verification": "1234"}}' http://heatseeknyc.com/readings.json



